import { Component, inject, OnInit, OnDestroy, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { GameService } from '../../services/game.service';
import { AttemptResult } from '../../models/game.models';

const COLORS = ['A', 'B', 'C', 'D', 'E', 'F'] as const;
type Color = typeof COLORS[number];

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss',
})
export class GameComponent implements OnInit, OnDestroy {
  private readonly gameService = inject(GameService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly COLORS = COLORS;
  readonly MAX_ATTEMPTS = 10;
  readonly CODE_LENGTH = 4;

  gameId = '';
  attempts = signal<AttemptResult[]>([]);
  currentGuess = signal<(Color | null)[]>([null, null, null, null]);
  selectedPosition = signal<number>(0);

  isFinished = signal(false);
  isWon = signal<boolean | null>(null);
  score = signal<number | null>(null);
  secretCode = signal<string | null>(null);
  errorMsg = signal('');
  submitting = signal(false);

  // Timer
  startTime = Date.now();
  elapsedSeconds = signal(0);
  private timerInterval: ReturnType<typeof setInterval> | null = null;

  readonly remainingAttempts = computed(() => this.MAX_ATTEMPTS - this.attempts().length);
  readonly rows = computed(() => {
    const filled = this.attempts();
    const result = [];
    for (let i = 0; i < this.MAX_ATTEMPTS; i++) {
      result.push(filled[i] ?? null);
    }
    return result;
  });

  ngOnInit(): void {
    this.gameId = this.route.snapshot.paramMap.get('id') ?? '';
    // Restore existing state if navigating back
    this.gameService.getGame(this.gameId).subscribe({
      next: (game) => {
        this.attempts.set(game.attempts ?? []);
        if (game.is_finished) {
          this.isFinished.set(true);
          this.isWon.set(game.is_won);
          this.score.set(game.score);
        }
      },
    });
    this.timerInterval = setInterval(() => {
      this.elapsedSeconds.set(Math.floor((Date.now() - this.startTime) / 1000));
    }, 1000);
  }

  ngOnDestroy(): void {
    if (this.timerInterval) clearInterval(this.timerInterval);
  }

  selectPosition(index: number): void {
    if (this.isFinished()) return;
    this.selectedPosition.set(index);
  }

  selectColor(color: Color): void {
    if (this.isFinished()) return;
    const guess = [...this.currentGuess()];
    guess[this.selectedPosition()] = color;
    this.currentGuess.set(guess);
    // Auto-advance to next empty slot
    const next = guess.findIndex((v, i) => i > this.selectedPosition() && v === null);
    if (next !== -1) this.selectedPosition.set(next);
    else {
      // find first empty overall
      const first = guess.findIndex((v) => v === null);
      if (first !== -1) this.selectedPosition.set(first);
    }
  }

  clearPosition(index: number): void {
    if (this.isFinished()) return;
    const guess = [...this.currentGuess()];
    guess[index] = null;
    this.currentGuess.set(guess);
    this.selectedPosition.set(index);
  }

  get isGuessComplete(): boolean {
    return this.currentGuess().every((c) => c !== null);
  }

  submitGuess(): void {
    if (!this.isGuessComplete || this.submitting() || this.isFinished()) return;

    const guessStr = (this.currentGuess() as Color[]).join('');
    this.submitting.set(true);
    this.errorMsg.set('');

    this.gameService.submitAttempt(this.gameId, guessStr).subscribe({
      next: (res) => {
        this.attempts.update((prev) => [...prev, res.attempt]);
        this.currentGuess.set([null, null, null, null]);
        this.selectedPosition.set(0);
        this.submitting.set(false);

        if (res.is_finished) {
          this.isFinished.set(true);
          this.isWon.set(res.is_won);
          this.score.set(res.score);
          this.secretCode.set(res.secret_code);
          if (this.timerInterval) clearInterval(this.timerInterval);
        }
      },
      error: (err) => {
        this.errorMsg.set(err?.error?.detail ?? 'Erro ao enviar tentativa.');
        this.submitting.set(false);
      },
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }

  formatTime(secs: number): string {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  pegsArray(n: number): number[] {
    return Array.from({ length: n });
  }

  emptyPegs(n: number): number[] {
    return Array.from({ length: 4 - n });
  }
}
