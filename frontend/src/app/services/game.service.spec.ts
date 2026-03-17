import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';
import { GameService } from './game.service';

describe('GameService', () => {
  let service: GameService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), GameService],
    });
    service = TestBed.inject(GameService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should be created', () => expect(service).toBeTruthy());

  it('should POST to /games/start', () => {
    service.startGame().subscribe((g) => expect(g.id).toBe('g1'));
    const req = httpMock.expectOne('http://localhost:8000/games/start');
    expect(req.request.method).toBe('POST');
    req.flush({ id: 'g1', user_id: 'u1', started_at: new Date().toISOString(), max_attempts: 10 });
  });

  it('should POST to /games/:id/attempt', () => {
    service.submitAttempt('g1', 'ABCD').subscribe((res) => {
      expect(res.attempt.guess).toBe('ABCD');
    });
    const req = httpMock.expectOne('http://localhost:8000/games/g1/attempt');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ guess: 'ABCD' });
    req.flush({
      attempt: { guess: 'ABCD', correct_position: 1, correct_color: 2 },
      attempt_number: 1,
      is_finished: false,
      is_won: false,
      score: null,
      secret_code: null,
      remaining_attempts: 9,
    });
  });

  it('should GET ranking', () => {
    service.getRanking().subscribe((r) => expect(r.length).toBe(1));
    const req = httpMock.expectOne('http://localhost:8000/ranking/');
    expect(req.request.method).toBe('GET');
    req.flush([{ rank: 1, user_id: 'u1', username: 'player', best_score: 900, total_games: 5, wins: 4 }]);
  });
});
