import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { AuthService } from './auth.service';
import { AuthStorageService } from './auth-storage.service';

describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;
  let storageSpy: jasmine.SpyObj<AuthStorageService>;

  beforeEach(() => {
    storageSpy = jasmine.createSpyObj('AuthStorageService', ['saveToken', 'getToken', 'clear', 'isAuthenticated']);

    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        AuthService,
        { provide: AuthStorageService, useValue: storageSpy },
      ],
    });

    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should call login endpoint and save token', () => {
    storageSpy.saveToken.and.stub();
    service.login({ username: 'user', password: 'pass' }).subscribe((res) => {
      expect(res.access_token).toBe('mock-token');
      expect(storageSpy.saveToken).toHaveBeenCalledWith('mock-token');
    });

    const req = httpMock.expectOne('http://localhost:8000/auth/login');
    expect(req.request.method).toBe('POST');
    req.flush({ access_token: 'mock-token', token_type: 'bearer' });
  });

  it('should call register endpoint', () => {
    service.register({ username: 'u', email: 'u@e.com', password: 'pass123' }).subscribe((user) => {
      expect(user.username).toBe('u');
    });

    const req = httpMock.expectOne('http://localhost:8000/auth/register');
    expect(req.request.method).toBe('POST');
    req.flush({ id: '1', username: 'u', email: 'u@e.com', created_at: new Date().toISOString() });
  });

  it('should clear storage on logout', () => {
    service.logout();
    expect(storageSpy.clear).toHaveBeenCalled();
  });
});
