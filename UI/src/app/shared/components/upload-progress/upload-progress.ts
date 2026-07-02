import { Component, Input } from '@angular/core';

@Component({

selector:'app-upload-progress',

standalone:true,

templateUrl:'./upload-progress.html',

styleUrl:'./upload-progress.scss'

})

export class UploadProgressComponent{

@Input()

step='Uploading';

}