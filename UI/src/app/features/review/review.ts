import {

Component,

inject,

signal

} from '@angular/core';

import { ClaimListComponent } from '../../shared/components/claim-list/claim-list';

import { PatientCardComponent } from '../../shared/components/patient-card/patient-card';

import { EvidenceCardComponent } from '../../shared/components/evidence-card/evidence-card';

import { SuggestionCardComponent } from '../../shared/components/suggestion-card/suggestion-card';

import { PromptService } from '../../core/services/prompt';

import { ReviewService } from '../../core/services/review';

import { NursePrompt } from '../../core/models/prompt';

import { EvaluationResult } from '../../core/models/evaluation-result';

@Component({

selector:'app-review',

standalone:true,

imports:[

ClaimListComponent,

PatientCardComponent,

EvidenceCardComponent,

SuggestionCardComponent

],

templateUrl:'./review.html',

styleUrl:'./review.scss'

})

export class ReviewComponent{

private promptService=inject(

PromptService

);

private reviewService=inject(

ReviewService

);

prompts=signal<NursePrompt[]>([]);



selectedPage=

signal(1);

pdfPath=

signal(

'assets/sample.pdf'

);

selectedPrompt=

signal<NursePrompt|null>(null);

result=

signal<EvaluationResult|null>(null);

constructor(){

this.loadPrompts();

}

loadPrompts(){

this.promptService

.getPrompts()

.subscribe({

next:data=>{

this.prompts.set(data);

},

error:console.error

});

}

openPdf(page:number){

    this.selectedPage.set(page);

}

selectPrompt(

prompt:NursePrompt

){

this.selectedPrompt.set(prompt);

this.reviewService

.evaluate(

'patient001',

prompt.prompt_id

)

.subscribe({

next:r=>{

this.result.set(r);

},

error:console.error

});

}

}