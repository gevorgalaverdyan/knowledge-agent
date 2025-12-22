import { Component } from '@angular/core';
import { LayoutComponent } from '../layout/layout.component';
import { FooterComponent } from '../layout/footer.component';

@Component({
  selector: 'app-footer',
  imports: [LayoutComponent, FooterComponent],
  templateUrl: './footer.html',
})
export class Footer {

}
