import ebs_snapshots.snapshot_manager as snapshot_manager
import unittest
import boto
from moto import mock_ec2

class TestSnapshotManager(unittest.TestCase):

    def _mock_true(*args, **kwargs):
        return True


    @mock_ec2
    def test_ignore_attached_volumes(self):
        conn = boto.connect_ec2('the_key', 'the_secret')

        # create some volumes
        volumes = [
                conn.create_volume(50, 'us-west-1a'),  # attached
                conn.create_volume(50, 'us-west-1a'),  # attachment exists but None
                conn.create_volume(50, 'us-west-1a')   # no attachment
                ]
        attachment = boto.ec2.volume.AttachmentSet()
        attachment.status = 'attached'
        volumes[0].attach_data = attachment  # add a connected status
        volumes[1].attach_data = boto.ec2.volume.AttachmentSet()  # add a None attachment

        # mock out details for snapshot_manager.run
        snapshot_manager._ensure_snapshot = self._mock_true
        snapshot_manager._remove_old_snapshots = self._mock_true

        # run function for all volumes
        for volume in volumes:
            snapshot_manager.run(conn, volume.id)

        # ensure is_volume_detached does not return volumes[0]
        self.assertFalse(snapshot_manager._is_volume_detached(volumes[0]))
        self.assertTrue(snapshot_manager._is_volume_detached(volumes[1]))
        self.assertTrue(snapshot_manager._is_volume_detached(volumes[2]))
