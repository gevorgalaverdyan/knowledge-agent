import { AfterViewInit, ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { Z_MODAL_DATA } from '../dialog/dialog.service';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ZardInputDirective } from '../input/input.directive';

export interface iDialogData {
  chat_title: string;
}

@Component({
  selector: 'app-create-chat-dialog',
  imports: [FormsModule, ReactiveFormsModule, ZardInputDirective],
  templateUrl: './create-chat-dialog.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  exportAs: 'createChatDialog',
})
export class CreateChatDialog implements AfterViewInit {
  private zData: iDialogData = inject(Z_MODAL_DATA);
 
  form = new FormGroup({
    chat_title: new FormControl(''),
  });
 
  ngAfterViewInit(): void {
    if (this.zData) {
      this.form.patchValue(this.zData);
    }
  }
}
