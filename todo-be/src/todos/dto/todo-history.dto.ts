import { ApiProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

export class TodoHistoryDto {
  @ApiProperty()
  @Expose()
  _id: string;

  @ApiProperty()
  @Expose()
  todoId: string;

  @ApiProperty()
  @Expose()
  changedAt: Date;

  @ApiProperty()
  @Expose()
  changes: Record<string, any>;
}
