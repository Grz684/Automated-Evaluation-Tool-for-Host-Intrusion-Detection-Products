import logging
import time
from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTask
from pyVmomi import vmodl, vim
import ssl
import sys


class RevertToSnapshot:

    def __init__(self, hostname, username, password, foldername, vmname, snapshot_name):
        self.username = username
        self.hostname = hostname
        self.password = password
        self.foldername = foldername
        self.vmname = vmname
        self.snapshot_name = snapshot_name

    def wait_for_task(self, task):
        while task.info.state == "running" or task.info.state == "queued":
            time.sleep(1)

        if task.info.state == "success":
            return
        logging.error('error message')

    def print_vm_info(self, virtual_machine):
        """
        Print information for a particular virtual machine or recurse into a
        folder with depth protection
        """
        summary = virtual_machine.summary
        print("Name       : ", summary.config.name)
        print("Template   : ", summary.config.template)
        print("Path       : ", summary.config.vmPathName)
        print("Guest      : ", summary.config.guestFullName)
        print("Instance UUID : ", summary.config.instanceUuid)
        print("Bios UUID     : ", summary.config.uuid)
        annotation = summary.config.annotation
        if annotation:
            print("Annotation : ", annotation)
        print("State      : ", summary.runtime.powerState)
        if summary.guest is not None:
            ip_address = summary.guest.ipAddress
            tools_version = summary.guest.toolsStatus
            if tools_version is not None:
                print("VMware-tools: ", tools_version)
            else:
                print("Vmware-tools: None")
            if ip_address:
                print("IP         : ", ip_address)
            else:
                print("IP         : None")
        if summary.runtime.question is not None:
            print("Question  : ", summary.runtime.question.text)
        print("")

    def get_snapshots_by_name_recursively(self, snapshots, snapname):
        snap_obj = []
        for snapshot in snapshots:
            if snapshot.name == snapname:
                snap_obj.append(snapshot)
            else:
                snap_obj = snap_obj + self.get_snapshots_by_name_recursively(
                    snapshot.childSnapshotList, snapname)
        return snap_obj

    def list_snapshots_recursively(self, snapshots):
        snapshot_data = []
        for snapshot in snapshots:
            snap_text = "Name: %s; Description: %s; CreateTime: %s; State: %s" % (
                snapshot.name, snapshot.description,
                snapshot.createTime, snapshot.state)
            snapshot_data.append(snap_text)
            snapshot_data = snapshot_data + self.list_snapshots_recursively(
                snapshot.childSnapshotList)
        return snapshot_data

    class TypeNotFoundException(Exception):
        def __init__(self, msg):
            self.msg = msg

    def get_obj(self, content, folder, vimtype: list, name: str):
        obj = None
        container = content.viewManager.CreateContainerView(folder, vimtype, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        if obj is None:
            raise self.TypeNotFoundException("did not find {} in {}".format(vimtype, folder))
        container.Destroy()
        return obj

    def revert(self):
        context = None
        if hasattr(ssl, '_create_unverified_context'):
            context = ssl._create_unverified_context()
        si = SmartConnect(host=self.hostname,
                          user=self.username,
                          pwd=self.password,
                          sslContext=context)
        if not si:
            print("Could not connect to the specified host using specified "
                  "username and password")
            sys.exit(1)
        else:
            """找到目标虚拟机"""
            print("Display info of target virtual machine")
            content = si.RetrieveContent()
            folder = self.get_obj(content, content.rootFolder, [vim.Folder], self.foldername)
            vm = self.get_obj(content, folder, [vim.VirtualMachine], self.vmname)
            self.print_vm_info(vm)

            """列出所有快照"""
            print("Display list of snapshots on virtual machine %s" % vm.name)
            snapshot_paths = self.list_snapshots_recursively(
                vm.snapshot.rootSnapshotList)
            for snapshot in snapshot_paths:
                print(snapshot)
            print("")

            """恢复到当前快照状态"""
            snap_obj = self.get_snapshots_by_name_recursively(
                vm.snapshot.rootSnapshotList, self.snapshot_name)
            # if len(snap_obj) is 0; then no snapshots with specified name
            if len(snap_obj) == 1:
                snap_obj = snap_obj[0].snapshot
                print("Reverting to snapshot %s ..." % self.snapshot_name)
                task = snap_obj.RevertToSnapshot_Task()
                self.wait_for_task(task)
                print("Success!\n")

            else:
                print("No snapshots found with name: %s on VM: %s" % (
                    self.snapshot_name, vm.name))
