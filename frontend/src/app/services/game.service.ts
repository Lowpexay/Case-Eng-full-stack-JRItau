import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  GameStart,
  Game,
  AttemptResponse,
  RankingEntry,
} from '../models/game.models';

@Injectable({ providedIn: 'root' })
export class GameService {
  private readonly http = inject(HttpClient);
  private readonly base = environment.apiUrl;

  startGame(): Observable<GameStart> {
    return this.http.post<GameStart>(`${this.base}/games/start`, {});
  }

  submitAttempt(gameId: string, guess: string): Observable<AttemptResponse> {
    return this.http.post<AttemptResponse>(`${this.base}/games/${gameId}/attempt`, { guess });
  }

  getGame(gameId: string): Observable<Game> {
    return this.http.get<Game>(`${this.base}/games/${gameId}`);
  }

  getMyGames(): Observable<Game[]> {
    return this.http.get<Game[]>(`${this.base}/games/`);
  }

  getRanking(): Observable<RankingEntry[]> {
    return this.http.get<RankingEntry[]>(`${this.base}/ranking/`);
  }
}
