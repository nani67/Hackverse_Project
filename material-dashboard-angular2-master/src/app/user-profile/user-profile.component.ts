import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {CollectionViewer, DataSource} from '@angular/cdk/collections';
import {Observable} from 'rxjs';
import { AngularFirestore } from 'angularfire2/firestore';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {


  @ViewChild('email', {static: true}) email: ElementRef;
  @ViewChild('fname', {static: true}) fname: ElementRef;
  @ViewChild('lname', {static: true}) lname: ElementRef;
  @ViewChild('bigInfo', {static: true}) bigInfo: ElementRef;

  constructor(public ups: AngularFirestore) { }

  ngOnInit() {
  }

  uploadUserProfile() {

    const titleOne = this.email.nativeElement.value;

    const descriptThree = this.bigInfo.nativeElement.value;

    const descript = this.fname.nativeElement.value + this.lname.nativeElement.value;

    const data = {
      'facultyName': descript,
      'About us': descriptThree,
      'email': titleOne,
    };


    this.ups.collection('TeachersLoginDetails').doc(Math.random() * 1000000 + '').set(data);

  }

}
