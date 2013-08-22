import os
import re
import datetime
import sqlite3
import re
import csv

re_server = re.compile(r"Testing from (.*) \((.*)\)")
re_host = re.compile(r"Hosted by (.*) \((.*)\) \[(.*) km\]\: (.*) ms")
re_download = re.compile(r"Download: (.*) Mbit")
re_upload = re.compile(r"Upload: (.*) Mbit")

def listserver():
    os.system("speedtest-cli --list > server.txt")

    re_line = re.compile(r"([\d]+)\) (.*) \((.*), (.*)\) \[(.*) km\]")
    vs = []
    with open("server.txt") as reader:
        for line in reader:
            p= re_line.findall(line)
            if p:
               vs.append(p[0])

    # sort with server id
    vs.sort(key=lambda i: i[0])
    return vs

def create_data_table():
    with sqlite3.connect("./speeddata.db") as conn:
        conn.execute("""
            create table if not exists speeddata(
                host text,
                test_time timestamp,
                test_status boolean,
                server_id integer,
                server_name text,
                server_location text,
                server_country text,
                server_distance float,
                server_test_from text,
                server_test_from_ip text,
                server_ping float,
                server_download float,
                server_upload float,
                unique(host, test_time, server_id)
            );
        """)
        conn.commit()


def test_server(server_id, log_path):
    try:
        os.system("speedtest-cli --server %s > %s" % (server_id, log_path))
        with open(log_path) as ifile:
            icontent = ifile.read()

            test_from, ip = re_server.findall(icontent)[0]
            host_name, location, distance, ping = re_host.findall(icontent)[0]
            download = re_download.findall(icontent)[0]
            upload = re_upload.findall(icontent)[0]

            return {
                "test_from": test_from,
                "ip": ip,
                "host_name": host_name,
                "location": location,
                "distance": distance,
                "ping": ping,
                "download": download,
                "upload": upload
            }
    except:
        return {}

def import_csv(csv_path):
    with open(csv_path) as ifile, sqlite3.connect("./speeddata.db") as conn:
        reader = csv.reader(ifile)

        for row in reader:
            conn.execute("""
                insert or ignore into speeddata(
                    host,
                    test_time,
                    test_status,
                    server_id,
                    server_name,
                    server_location,
                    server_country,
                    server_distance,
                    server_test_from,
                    server_test_from_ip,
                    server_ping,
                    server_download,
                    server_upload
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, row)

        conn.commit()


def speed_test(host, country="Taiwan"):
    servers = listserver()
    utc_time = datetime.datetime.utcnow()
    timestamp = utc_time.strftime("%Y%m%d/%H%M%S")

    log_folder = "./log/%s/%s/%s/" % (host, timestamp, country)
    csv_path = "./%s.csv" % host

    os.makedirs(log_folder)

    with open(csv_path,'a') as ifile:
        writer = csv.writer(ifile)

        for server in servers:
            server_id, name, location, country_code, distance = server

            if country_code == country:
                print "start testing", server
                filepath = "%s/%s.log" % (log_folder, server_id)

                vs = test_server(server_id, filepath)

                writer.writerow([
                    host,
                    utc_time,
                    True if vs else False,
                    server_id,
                    name,
                    location,
                    country_code,
                    distance,
                    vs.get("test_from"),
                    vs.get("ip"),
                    vs.get("ping"),
                    vs.get("download"),
                    vs.get("upload")
                ])

if __name__ == "__main__":
    import clime.now
