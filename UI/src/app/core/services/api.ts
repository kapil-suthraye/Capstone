import { Injectable, inject } from '@angular/core';

import {

HttpClient,

HttpHeaders

} from '@angular/common/http';

import { environment } from '../../../environments/environment';

@Injectable({

providedIn:'root'

})

export class ApiService{

private http=inject(HttpClient);

private url=environment.apiUrl;

get<T>(endpoint:string){

return this.http.get<T>(

`${this.url}/${endpoint}`

);

}

post<T>(

endpoint:string,

body:any

){

return this.http.post<T>(

`${this.url}/${endpoint}`,

body

);

}

upload(

file:File

){

const form=new FormData();

form.append(

'file',

file

);

return this.http.post(

`${this.url}/upload`,

form

);

}

}