import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { DependencyStatus } from '../types';
import { TodoBaseDto } from './todo-base.dto';

export class TodoResponseDto extends TodoBaseDto {
  @ApiProperty({ example: '67e6d0fd2f6b9d3f7d8d1234' })
  _id: string;

  @ApiPropertyOptional({
    enum: DependencyStatus,
    example: DependencyStatus.BLOCKED,
  })
  dependencyStatus?: DependencyStatus;

  @ApiProperty({
    example: '2026-03-29T10:00:00.000Z',
    format: 'date-time',
  })
  createdAt: string;

  @ApiProperty({
    example: '2026-03-29T10:30:00.000Z',
    format: 'date-time',
  })
  updatedAt: string;

  @ApiPropertyOptional({
    example: null,
    nullable: true,
    format: 'date-time',
  })
  deletedAt?: string | null;
}

export class TodoSearchResponseDto {
  @ApiProperty({ example: 12 })
  total: number;

  @ApiProperty({ example: 1 })
  page: number;

  @ApiProperty({ example: 10 })
  limit: number;

  @ApiProperty({ type: () => TodoResponseDto, isArray: true })
  results: TodoResponseDto[];
}
