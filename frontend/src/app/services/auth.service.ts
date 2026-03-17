import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import { environment } from '../../environments/environment';
import { AuthStorageService } from './auth-storage.service';
import {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
} from '../models/game.models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly storage = inject(AuthStorageService);
  private readonly base = environment.apiUrl;

  login(data: LoginRequest): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.base}/auth/login`, data).pipe(
      tap((res) => this.storage.saveToken(res.access_token))
    );
  }

  register(data: RegisterRequest): Observable<User> {
    return this.http.post<User>(`${this.base}/auth/register`, data);
  }

  getMe(): Observable<User> {
    return this.http.get<User>(`${this.base}/users/me`);
  }

  logout(): void {
    this.storage.clear();
  }

  isAuthenticated(): boolean {
    return this.storage.isAuthenticated();
  }
}
