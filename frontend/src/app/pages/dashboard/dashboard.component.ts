import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { GameService } from '../../services/game.service';
import { User, Game } from '../../models/game.models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit, OnDestroy {
  private readonly auth = inject(AuthService);
  private readonly gameService = inject(GameService);
  private readonly router = inject(Router);

  user = signal<User | null>(null);
  recentGames = signal<Game[]>([]);
  loadingGame = signal(false);
  errorMsg = signal('');
  greeting = signal('Olá');

  private greetingTimer?: number;

  ngOnInit(): void {
    this.updateGreeting();
    this.greetingTimer = window.setInterval(() => this.updateGreeting(), 60_000);

    this.auth.getMe().subscribe({
      next: (u) => this.user.set(u),
      error: () => this.logout(),
    });
    this.gameService.getMyGames().subscribe({
      next: (games) => this.recentGames.set(games.slice(0, 5)),
    });
  }

  ngOnDestroy(): void {
    if (this.greetingTimer) {
      window.clearInterval(this.greetingTimer);
    }
  }

  startGame(): void {
    this.loadingGame.set(true);
    this.errorMsg.set('');
    this.gameService.startGame().subscribe({
      next: (game) => this.router.navigate(['/game', game.id]),
      error: (err) => {
        this.errorMsg.set(err?.error?.detail ?? 'Erro ao iniciar partida.');
        this.loadingGame.set(false);
      },
    });
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  formatDuration(secs: number | null): string {
    if (secs == null) return '—';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return m > 0 ? `${m}m ${s}s` : `${s}s`;
  }

  private updateGreeting(): void {
    const hour = new Date().getHours();
    if (hour < 12) {
      this.greeting.set('Bom dia');
      return;
    }
    if (hour < 18) {
      this.greeting.set('Boa tarde');
      return;
    }
    this.greeting.set('Boa noite');
  }
}
