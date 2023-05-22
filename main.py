import reddit
import db
import signal, sys
# handle sigint
def signal_handler(sig, frame):
    # cleanup here
    print('\nExiting...')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    if __name__=='__main__':
        # db.init('reddit.db')
        reddit.query_popular_nsfw(10, 10)

main()