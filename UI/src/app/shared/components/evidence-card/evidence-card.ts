import {

Component,

Input,

Output,

EventEmitter

} from '@angular/core';

import { EvaluationResult }

from '../../../core/models/evaluation-result';

import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';

import { MatExpansionModule } from '@angular/material/expansion';

import { MatButtonModule } from '@angular/material/button';

@Component({

selector:'app-evidence-card',

standalone:true,

templateUrl:'./evidence-card.html',

styleUrl:'./evidence-card.scss',

imports:[

CommonModule,

MatCardModule,

MatExpansionModule,

MatButtonModule

]

})

export class EvidenceCardComponent{

@Input(

{

required:true

}

)

result!:EvaluationResult;

@Output()

openEvidence = new EventEmitter<number>();

}