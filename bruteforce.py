import rarfile, zipfile
from threading import Thread
import optparse
import itertools
import time

rarfile.UNRAR_TOOL = "unrar"


def bruteforce(charset, minlength, maxlength):
    return (''.join(candidate)
            for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
                                                           for i in range(minlength, maxlength + 1)))


def extractFile(arFile, attempt):
    try:
        arFile.extractall(pwd=attempt)
        print "Password found! password is %s" % attempt
        exit(0)
    except Exception, e:
        pass


def main():
    parser = optparse.OptionParser("usage%prog -f <file, zip or rar> -c <charset> -n <size>")
    parser.add_option('-f', dest='name', type='string', help='specify file')
    parser.add_option('-c', dest='charset', type='string', help='specify charset')
    parser.add_option('-s', dest='start_size', default=1, type='int', help='start size of password, default = 1')
    parser.add_option('-e', dest='end_size', type='int', help='end size of password')
    parser.add_option('-t', dest='threads', type='int', default=0, help='use threads or not')
    (options, args) = parser.parse_args()
    if not options.name or not options.charset or not options.end_size:
        print parser.usage
        exit(0)
    else:
        start = time.clock()
        arname = options.name
        if arname.lower().endswith('.rar'):
            arFile = rarfile.RarFile(arname)
        elif arname.lower().endswith('.zip'):
            arFile = zipfile.ZipFile(arname)
        else:
            print '<file> needs to be ended with ".zip" or ".rar"!'
            exit(0)
        charset = options.charset
        start_size = options.start_size
        end_size = options.end_size
        password_list = bruteforce(charset, start_size, end_size)
        total_num = sum([len(charset)**x for x in range(start_size, end_size+1)])
        last_report_t = 0
        for idx, attempt in enumerate(password_list):
            # match it against your password, or whatever
            if options.threads == 1:
                t = Thread(target=extractFile, args=(arFile,attempt))
                t.start()
            else:
                extractFile(arFile, attempt)
            percent = idx * 100.0 / total_num
            elapsed_sec = time.clock() - start
            if int(elapsed_sec) % 10 == 0:
                if elapsed_sec - last_report_t > 1.0:
                    estimate_t = elapsed_sec * (100-percent) / percent
                    last_report_t = elapsed_sec
                    print 'At %s, %d%%, estimate finish time: %.2f hours.' % (attempt, percent, estimate_t/3600)


if __name__ == '__main__':
    main()