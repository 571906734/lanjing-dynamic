#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚢 LanJing Ship Service${NC}"
echo "============================"

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment ready${NC}"
fi

echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}.env created from template${NC}"
fi

if [ ! -f "instance/lanjing.db" ]; then
    echo -e "${YELLOW}Initializing database...${NC}"
    python admin_setup.py
fi

echo -e "${GREEN}Starting at http://localhost:5000${NC}"
echo -e "${GREEN}Admin: admin@lanjing.com / admin123${NC}"
echo "============================"

python app.py