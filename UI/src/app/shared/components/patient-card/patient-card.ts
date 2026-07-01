import { Component } from '@angular/core';

import { MatCardModule } from '@angular/material/card';

@Component({

selector:'app-patient-card',

standalone:true,

imports:[

MatCardModule

],

templateUrl:'./patient-card.html',

styleUrl:'./patient-card.scss'

})

export class PatientCardComponent{}