export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export interface AttemptResult {
  guess: string;
  correct_position: number;
  correct_color: number;
}

export interface GameStart {
  id: string;
  user_id: string;
  started_at: string;
  max_attempts: number;
}

export interface Game {
  id: string;
  user_id: string;
  attempts: AttemptResult[];
  attempt_count: number;
  max_attempts: number;
  score: number | null;
  duration_seconds: number | null;
  started_at: string;
  finished_at: string | null;
  is_won: boolean | null;
  is_finished: boolean;
}

export interface AttemptResponse {
  attempt: AttemptResult;
  attempt_number: number;
  is_finished: boolean;
  is_won: boolean;
  score: number | null;
  secret_code: string | null;
  remaining_attempts: number;
}

export interface RankingEntry {
  rank: number;
  user_id: string;
  username: string;
  best_score: number;
  total_games: number;
  wins: number;
}
