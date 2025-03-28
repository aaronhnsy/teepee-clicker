#!/bin/bash

DIR="$HOME/projects/teepee-clicker/"

if tmux has-session -t teepee 2>/dev/null; then
    tmux kill-session -t teepee
fi

tmux new-session -d -s teepee -n backend -c "$DIR/backend"
tmux send-keys -t teepee:backend "clear && litestar --app src:teepee run --debug --reload --host 127.0.0.1 --port 10000" C-m

tmux new-window -d -n frontend -c "$DIR/frontend"
tmux send-keys -t teepee:frontend "clear && npm run dev" C-m

tmux new-window -d -n pyright -c "$DIR/backend"
tmux send-keys -t teepee:pyright "clear && pyright -w" C-m

tmux new-window -d -n misc -c "$DIR"
tmux send-keys -t teepee:misc "tailscale serve --bg --set-path / http://127.0.0.1:10001" C-m
tmux send-keys -t teepee:misc "tailscale serve --bg --set-path /api http://127.0.0.1:10000/api" C-m
tmux send-keys -t teepee:misc "tailscale serve --bg --set-path /websocket http://127.0.0.1:10000/websocket" C-m

tmux attach-session -t teepee
