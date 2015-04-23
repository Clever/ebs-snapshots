from ebs_snapshots import ebs_snapshots_daemon
import sys
import kayvee
import logging

if __name__ == "__main__":
    try:
        ebs_snapshots_daemon.snapshot_timer()
    except Exception as e:
        logging.info(kayvee.formatLog("ebs-snapshots", "error", "unknown exception", {"error": str(e)}))
        sys.exit(1)
