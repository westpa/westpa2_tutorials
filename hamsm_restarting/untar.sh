# This *intentionally* is not marked executable, and does not have a hashbang..
# There's something weird that happens with backgrounding that tar process, at
#       least on the machine I'm developing this on, and launching with `./untar.sh`
#       instead of `bash untar.sh`


echo "This should be run from the haMSM tutorial WEST_SIM_ROOT!"

echo "Untarring $1"

tar --totals=USR1 -xzf $1 &
pid=$!

# If this script is killed, kill the `tar'.
trap "kill $pid 2> /dev/null" EXIT

# While copy is running...
while kill -0 $pid 2> /dev/null; do
    # Do stuff
    echo -n -e "\e[2A\e[K"
    pkill -SIGUSR1 tar
    sleep 0.5
    echo -e "\e[KTotal: ~ 2.7 GiB"
    sleep 1
done

echo "Done"
# Disable the trap on a normal exit.
trap - EXIT

