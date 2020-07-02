import os
import errno


def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

#StarLink constellation: 1584 satellites into 72 orbital planes of 22 satellites each
def main():
    orbital_plane_num=72;
    satellite_per_plan=22;
    for orbit_number in range(orbital_plane_num):
        filename = "starlink/" + "orbit_" + str(orbit_number) + "/docker-compose.yml";
        create_file_if_not_exit(filename);
        f = open(filename, "w+")
        # prepare version
        version = "version: '3'\n";
        f.write(version);
        f.write("services:\n");
        # prepare service
        for satellite_number in range(satellite_per_plan):
            container = "  StarLink-Orbit-" + str(orbit_number) + "-Satellite-" + str(satellite_number) + \
                        ":\n" \
                        "    image: ubuntu16_04\n" \
                        "    tty: true\n" \
                        "\n";
            f.write(container);
        # close file.
        f.close();

if __name__== "__main__":
  main()