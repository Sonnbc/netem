from numpy import random as rd
import sys, os

SIZE = 100000
device = "eth2"

def main(mean, sigma):
    a = [str(int(x)) for x in rd.lognormal(mean, sigma, SIZE)]
    with open("/tmp/lognormal.txt", "w") as f:
        print >> f, " ".join(a)

    make_table_cmd = "./iproute2/netem/maketable /tmp/lognormal.txt \
        > /usr/lib/tc/lognormal.dist"
    stats_cmd = "./iproute2/netem/stats /tmp/lognormal.txt | \
        awk '{if ($1 ==\"mu\" || $1 == \"sigma\") print $3}' \
        > /tmp/musigma.txt"   

    os.system(make_table_cmd)
    os.system(stats_cmd)

    with open("/tmp/musigma.txt") as f:
        mu = f.readline().split()[0]
        sigma = f.readline().split()[0]
        print ("mean = %s, sd = %s" % (mu, sigma))

    tc_cmd = "tc qdisc replace dev %s root netem delay \
        %sms %sms distribution lognormal" % (device, mu, sigma)
    print(tc_cmd)
    os.system(tc_cmd)

if __name__ == '__main__':
    mean = (sys.argv[1])
    sigma = (sys.argv[2])
    main(mean, sigma)