import {

Component,

Input

} from '@angular/core';

import {

EvaluationResult

}

from '../../../core/models/evaluation-result';

@Component({

selector:'app-suggestion-card',

standalone:true,

templateUrl:'./suggestion-card.html',

styleUrl:'./suggestion-card.scss'

})

export class SuggestionCardComponent{

@Input(

{

required:true

}

)

result!:EvaluationResult;

}