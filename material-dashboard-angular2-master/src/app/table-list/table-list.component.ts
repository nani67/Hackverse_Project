import { Component, OnInit } from '@angular/core';
import { ItemService } from '../services/item.service';

import { AngularFirestore } from 'angularfire2/firestore';

@Component({
  selector: 'app-table-list',
  templateUrl: './table-list.component.html',
  styleUrls: ['./table-list.component.css']
})
export class TableListComponent implements OnInit {
  items: Item[];

  constructor(private itemService: ItemService) {
  }

  ngOnInit() {
    this.itemService.getItems().subscribe(items => {
      this.items = items;
    });

  }

}

interface Item {
  ids?: string;
}
