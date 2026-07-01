import { Component, Input } from '@angular/core';

import { NgxExtendedPdfViewerModule }
from 'ngx-extended-pdf-viewer';

@Component({

selector:'app-pdf-viewer',

standalone:true,

imports:[

NgxExtendedPdfViewerModule

],

templateUrl:'./pdf-viewer.html',

styleUrl:'./pdf-viewer.scss'

})

export class PdfViewerComponent{

@Input()

src='';

@Input()

page=1;

}