import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss',
})
export class RegisterComponent {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);

  username = '';
  email = '';
  password = '';
  loading = signal(false);
  errorMsg = signal('');
  successMsg = signal('');

  onSubmit(form: NgForm): void {
    if (form.invalid) return;
    this.loading.set(true);
    this.errorMsg.set('');
    this.successMsg.set('');

    this.auth.register({ username: this.username, email: this.email, password: this.password }).subscribe({
      next: () => {
        this.successMsg.set('Conta criada! Redirecionando para o login...');
        setTimeout(() => this.router.navigate(['/login']), 1500);
      },
      error: (err) => {
        this.errorMsg.set(err?.error?.detail ?? 'Erro ao criar conta. Tente novamente.');
        this.loading.set(false);
      },
    });
  }
}
