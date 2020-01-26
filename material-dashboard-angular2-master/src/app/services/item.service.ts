import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from 'angularfire2/firestore';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ItemService {
  itemsCollection: AngularFirestoreCollection<Item>;
  items: Observable<any[]>;

  constructor(public afs: AngularFirestore) {
    this.items = this.afs.collection('UsersInfo').doc('RHZ1Se4HaeR22E4vdJemmTQfnDF3').collection('personalInfo').valueChanges();
  }

  getItems() {
    return this.items;
  }

}

interface Item {
  ids?: string;
}
