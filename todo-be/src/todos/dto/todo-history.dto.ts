import { ApiProperty } from '@nestjs/swagger';
import { TodoHistoryChangeBy, TodoStatus } from '../types';

export class TodoHistoryDto {
  @ApiProperty()
  _id: string;

  @ApiProperty()
  todoId: string;

  @ApiProperty({ enum: TodoStatus, example: TodoStatus.IN_PROGRESS })
  from: TodoStatus;

  @ApiProperty({ enum: TodoStatus, example: TodoStatus.COMPLETED })
  to: TodoStatus;

  @ApiProperty({
    enum: TodoHistoryChangeBy,
    example: TodoHistoryChangeBy.MANUAL,
  })
  by: TodoHistoryChangeBy;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;
}
