import { PartialType } from '@nestjs/swagger';
import { IsNotEmpty, IsString } from 'class-validator';
import { TodoBaseDto } from './todo-base.dto';

export class CreateTodoDto extends PartialType(TodoBaseDto) {
  @IsString()
  @IsNotEmpty()
  name: string;
}
