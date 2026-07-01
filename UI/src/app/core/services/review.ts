import { Injectable, inject } from '@angular/core';

import { ApiService } from './api';

import { EvaluationResult } from '../models/evaluation-result';

import { Observable } from 'rxjs';

@Injectable({

providedIn:'root'

})

export class ReviewService{

private api=inject(ApiService);

evaluate(

namespace:string,

promptId:string

):Observable<EvaluationResult>{

return this.api.post<EvaluationResult>(

'evaluate',

{

namespace,

prompt_id:promptId

}

);

}

}