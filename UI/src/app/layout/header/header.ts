import { Component } from '@angular/core';

import { MatIconModule } from '@angular/material/icon';

import { MatFormFieldModule } from '@angular/material/form-field';

import { MatInputModule } from '@angular/material/input';

@Component({

selector:'app-header',

standalone:true,

imports:[
MatIconModule,
MatFormFieldModule,
MatInputModule
],

templateUrl:'./header.html',

styleUrl:'./header.scss'

})

export class HeaderComponent{}