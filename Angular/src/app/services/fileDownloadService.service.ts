import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileDownloadService {

  constructor(private http: HttpClient) { }

  downloadFile(): Observable<Blob>  {
    return this.http.get('http://localhost:5000/download', { responseType: 'blob' })
    .pipe(
      catchError(error => {
        console.error('Download error:', error);
        // Display or handle error accordingly
        return throwError(error);
      })
    );
  }
}