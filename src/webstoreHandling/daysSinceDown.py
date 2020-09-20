
def main():
    getDates()


def getDates():
    with open('down_versions.txt') as inF:
        timestamps = inF.read().splitlines()
    d = {}
    currentTime = 2020*365 + 3*30 + 20
    for ts in sorted(timestamps):
        ts = ts.split(' ')[0]
        hid = ts.split('-')[0]
        times = ts.split('-')[1:]
        d[hid] = currentTime - (int(times[0])*365 + int(times[1])*30 + int(times[2]))
    recently_down_counter = 0
    recently_in_days = 365
    sum_total = 0
    for k,v in d.iteritems():
        sum_total += v
        if(v < 180):
            recently_down_counter += 1
    print(sum_total)
    print(len(d))
    print('average days = %d' % (int(sum_total)/len(d)))
    print('taken down in last %d days = %d' % (recently_in_days, recently_down_counter))
    # for k,v in d.iteritems():
    #     print(d[k])
    #     print(k)

if __name__ == '__main__':
    main()