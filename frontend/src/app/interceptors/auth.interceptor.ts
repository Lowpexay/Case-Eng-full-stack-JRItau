import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthStorageService } from '../services/auth-storage.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const storage = inject(AuthStorageService);
  const router = inject(Router);
  const token = storage.getToken();

  const request = token
    ? req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    })
    : req;

  return next(request).pipe(
    catchError((error) => {
      const isUnauthorized = error?.status === 401;
      const isLoginRoute = error?.url?.includes('/auth/login');

      if (isUnauthorized && !isLoginRoute) {
        storage.clear();
        router.navigate(['/login']);
      }

      return throwError(() => error);
    })
  );
};
