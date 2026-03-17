import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

type ThemeMode = 'dark' | 'light';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `
    <router-outlet />
    <button
      type="button"
      class="theme-toggle"
      (click)="toggleTheme()"
      [attr.aria-label]="theme() === 'dark' ? 'Ativar tema claro' : 'Ativar tema escuro'"
    >
      {{ theme() === 'dark' ? '☀️ Tema claro' : '🌙 Tema escuro' }}
    </button>
  `,
  styles: [
    `
      .theme-toggle {
        position: fixed;
        right: 1rem;
        bottom: 1rem;
        z-index: 999;
        border: 1px solid rgba(255, 255, 255, 0.16);
        background: var(--surface);
        color: var(--text);
        border-radius: 999px;
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: var(--shadow);
      }

      .theme-toggle:hover {
        transform: translateY(-1px);
      }
    `,
  ],
})
export class App {
  private static readonly THEME_STORAGE_KEY = 'mastermind-theme';

  readonly theme = signal<ThemeMode>(this.getInitialTheme());

  constructor() {
    this.applyTheme(this.theme());
  }

  toggleTheme(): void {
    const nextTheme: ThemeMode = this.theme() === 'dark' ? 'light' : 'dark';
    this.theme.set(nextTheme);
    this.applyTheme(nextTheme);
    localStorage.setItem(App.THEME_STORAGE_KEY, nextTheme);
  }

  private applyTheme(theme: ThemeMode): void {
    document.documentElement.setAttribute('data-theme', theme);
  }

  private getInitialTheme(): ThemeMode {
    const stored = localStorage.getItem(App.THEME_STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }

    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
}
