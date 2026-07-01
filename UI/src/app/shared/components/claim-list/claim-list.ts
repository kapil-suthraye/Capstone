import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-claim-list',
  standalone: true,
  templateUrl: './claim-list.html',
  styleUrl: './claim-list.scss'
})
export class ClaimListComponent {

  claims = signal([

    {
      id: 'CLM-1001',
      patient: 'John Smith',
      diagnosis: 'CHF',
      status: 'Pending'
    },

    {
      id: 'CLM-1002',
      patient: 'Mary Brown',
      diagnosis: 'Sepsis',
      status: 'Completed'
    },

    {
      id: 'CLM-1003',
      patient: 'David Wilson',
      diagnosis: 'Stroke',
      status: 'Pending'
    }

  ]);

}