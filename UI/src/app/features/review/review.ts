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

import { SessionService } from '../../core/services/session';

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

private session = inject(
    SessionService
);

private reviewService=inject(

ReviewService

);

prompts=signal<NursePrompt[]>([]);



selectedPage=

signal(1);

pdfPath = signal('');

selectedPrompt=

signal<NursePrompt|null>(null);

result=

signal<EvaluationResult|null>(null);

constructor(){

this.loadPrompts();
this.pdfPath.set(this.session.pdfPath);
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
    prompt: NursePrompt
): void {

    console.log(
    'Namespace =',
    this.session.namespace
    );
    this.selectedPrompt.set(prompt);

    console.log('Selected Prompt', prompt.prompt_id);

console.log('Namespace', this.session.namespace);

    this.reviewService.evaluate(

        this.session.namespace,

        prompt.prompt_id

    ).subscribe({

        next: result => {

            console.log(result);

            this.result.set(result);

        },

        error: error => {

            console.error(error);

        }

    });

}

}