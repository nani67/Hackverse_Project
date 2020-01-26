import {Component, ElementRef, Inject, OnInit, ViewChild} from '@angular/core';

import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from 'angularfire2/firestore';
import {DOCUMENT} from '@angular/common';



@Component({
  selector: 'app-typography',
  templateUrl: './typography.component.html',
  styleUrls: ['./typography.component.css']
})
export class TypographyComponent implements OnInit {


  @ViewChild('title', {static: true}) title: ElementRef;
  @ViewChild('desc', {static: true}) desc: ElementRef;

  constructor(private ups: AngularFirestore) {}



  updateValues() {

    let titleOne = this.title.nativeElement.value;
    let descript = this.desc.nativeElement.value;

    const data = {
      'UniversityClass': 'CSE',
      'UniversityName': 'GRIET',
      'reminder': descript,
      'section': 'F',
    };

    titleOne = '';
    descript = '';

    this.ups.collection('TeachersAssignmentsList').doc(Math.random() * 1000000 + '').set(data);

  }
  onSubmission() {
    return this.title;
  }

  ngOnInit() {
  }


}
