/*
  # Create Tickets Table for Discord Bot

  1. New Tables
    - `tickets`
      - `id` (uuid, primary key) - Unique ticket identifier
      - `ticket_number` (integer, unique) - Sequential ticket number for display
      - `discord_user_id` (text) - Discord user ID who created the ticket
      - `discord_username` (text) - Discord username
      - `channel_id` (text) - Discord channel ID for the ticket
      - `service_type` (text) - Type of service requested
      - `service_details` (text) - Detailed description of service
      - `budget` (text) - User's budget
      - `timeline` (text) - Expected timeline
      - `additional_info` (text) - Any additional information
      - `status` (text) - Ticket status (open, in_progress, closed)
      - `created_at` (timestamptz) - When ticket was created
      - `closed_at` (timestamptz) - When ticket was closed
  
  2. Security
    - Enable RLS on `tickets` table
    - Add policy for authenticated users to read all tickets
    - Add policy for authenticated users to insert tickets
    - Add policy for authenticated users to update tickets
*/

CREATE TABLE IF NOT EXISTS tickets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_number serial UNIQUE,
  discord_user_id text NOT NULL,
  discord_username text NOT NULL,
  channel_id text NOT NULL,
  service_type text NOT NULL,
  service_details text DEFAULT '',
  budget text DEFAULT '',
  timeline text DEFAULT '',
  additional_info text DEFAULT '',
  status text DEFAULT 'open',
  created_at timestamptz DEFAULT now(),
  closed_at timestamptz
);

ALTER TABLE tickets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow authenticated users to read tickets"
  ON tickets
  FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "Allow authenticated users to insert tickets"
  ON tickets
  FOR INSERT
  TO authenticated
  WITH CHECK (true);

CREATE POLICY "Allow authenticated users to update tickets"
  ON tickets
  FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Allow authenticated users to delete tickets"
  ON tickets
  FOR DELETE
  TO authenticated
  USING (true);

CREATE INDEX IF NOT EXISTS idx_tickets_discord_user_id ON tickets(discord_user_id);
CREATE INDEX IF NOT EXISTS idx_tickets_channel_id ON tickets(channel_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);