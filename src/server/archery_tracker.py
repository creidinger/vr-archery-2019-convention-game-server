import triad_openvr
import time
import sys


def track_tackers():
    '''
        Get tracker name, unique ID and position for all detected trackers
    '''

    v = triad_openvr.triad_openvr()
    # list of trackers as an array
    trackers = v.object_names["Tracker"]

    if len(sys.argv) == 1:
        interval = 1 / 250
    elif len(sys.argv) == 2:
        interval = 1 / float(sys.argv[0])
    else:
        return "Invalid number of arguments"
        interval = False

    if interval:
        while(True):

            data = ""

            # for each tracker
            for t in trackers:

                # tracker name and unique ID
                tracker_str = t + "|" + v.devices[t].get_serial()

                start = time.time()
                txt = ""

                # get position of each tracker
                for t in v.devices[t].get_pose_euler():
                    txt += "%.4f" % t
                    txt += "|"

                # appenda tracker data before returning
                data = data + tracker_str + "|" + txt + "&"

                sleep_time = interval - (time.time() - start)

                if sleep_time > 0:
                    time.sleep(sleep_time)

            # output position and tracker name
            # logging.info(data)
            return data

    else:
        # logging.info("Invalid number of arguments")
        return "Invalid number of arguments"
        interval = False
