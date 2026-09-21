#!/bin/bash
# Agent Reach activation script
# Ativa o ambiente virtual do Agent Reach e executa o comando

source ~/.agent-reach-venv/bin/activate
agent-reach "$@"
