import { TestBed } from '@angular/core/testing';
import { AuthStorageService } from './auth-storage.service';

describe('AuthStorageService', () => {
  let service: AuthStorageService;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [AuthStorageService] });
    service = TestBed.inject(AuthStorageService);
  });

  it('should save and retrieve token', () => {
    service.saveToken('my-token');
    expect(service.getToken()).toBe('my-token');
    expect(service.isAuthenticated()).toBeTrue();
  });

  it('should clear token', () => {
    service.saveToken('my-token');
    service.clear();
    expect(service.getToken()).toBeNull();
    expect(service.isAuthenticated()).toBeFalse();
  });

  it('should save and retrieve user', () => {
    service.saveUser({ id: '1', username: 'test' });
    const user = service.getUser<{ id: string; username: string }>();
    expect(user?.username).toBe('test');
  });
});
