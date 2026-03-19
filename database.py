import json
import os
from typing import Optional, Dict, Any
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), 'tickets.json')


class DatabaseManager:
    def __init__(self):
        self._load_data()

    def _load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                self._data = json.load(f)
        else:
            self._data = {'tickets': [], 'next_ticket_number': 1}

    def _save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self._data, f, indent=2)

    def create_ticket(self, ticket_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            ticket_data['ticket_number'] = self._data['next_ticket_number']
            ticket_data['created_at'] = datetime.utcnow().isoformat()
            self._data['next_ticket_number'] += 1
            self._data['tickets'].append(ticket_data)
            self._save_data()
            return ticket_data
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return None

    def get_ticket_by_channel_id(self, channel_id: str) -> Optional[Dict[str, Any]]:
        try:
            for ticket in self._data['tickets']:
                if ticket['channel_id'] == channel_id:
                    return ticket
            return None
        except Exception as e:
            print(f"Error getting ticket: {e}")
            return None

    def update_ticket_status(self, channel_id: str, status: str, closed_at: Optional[str] = None) -> bool:
        try:
            for ticket in self._data['tickets']:
                if ticket['channel_id'] == channel_id:
                    ticket['status'] = status
                    if closed_at:
                        ticket['closed_at'] = closed_at
                    self._save_data()
                    return True
            return False
        except Exception as e:
            print(f"Error updating ticket: {e}")
            return False

    def get_user_tickets(self, discord_user_id: str) -> list:
        try:
            return sorted(
                [t for t in self._data['tickets'] if t['discord_user_id'] == discord_user_id],
                key=lambda t: t.get('created_at', ''),
                reverse=True
            )
        except Exception as e:
            print(f"Error getting user tickets: {e}")
            return []

    def get_all_open_tickets(self) -> list:
        try:
            return sorted(
                [t for t in self._data['tickets'] if t['status'] == 'open'],
                key=lambda t: t.get('created_at', ''),
                reverse=True
            )
        except Exception as e:
            print(f"Error getting open tickets: {e}")
            return []