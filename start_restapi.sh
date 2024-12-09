echo "Updating system packages..."
sudo apt update -y

echo "Installing Python and pip..."
sudo apt install python3 python3-pip -y
sudo apt install tmux


pip3 install -r requirements.txt

tmux new-session -d -s restapi
tmux split-window -h
tmux send-keys "python3 -m uvicorn server:app --reload" C-m
tmux select-pane -t 0
tmux send-keys "python3 client.py" C-m

tmux attach -t restapi



