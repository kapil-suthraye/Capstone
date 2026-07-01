import {

Component,

inject,

signal

} from '@angular/core';

import { UploadService } from '../../../core/services/upload';

@Component({

  selector: 'app-upload-card',

  standalone: true,

  templateUrl: './upload-card.html',

  styleUrl: './upload-card.scss'

})

export class UploadComponent{

private service=inject(

UploadService

);

uploading=signal(false);

select(

event:any

){

const file=

event.target.files[0];

if(!file)

return;

this.uploading.set(true);

this.service

.upload(file)

.subscribe({

next:()=>{

this.uploading.set(false);

},

error:()=>{

this.uploading.set(false);

}

});

}

}