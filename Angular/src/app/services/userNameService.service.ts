import { Injectable } from "@angular/core";

@Injectable()
export class UserNameService {
  Name: string;

  set user_name(value: string) {
    this.Name = value;
  }

  get user_name(): string {
    return this.Name;
  }

  constructor() {}
}
