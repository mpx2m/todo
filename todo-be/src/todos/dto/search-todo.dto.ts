import { ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsDateString,
  IsEnum,
  IsInt,
  IsOptional,
  IsString,
  Min,
} from 'class-validator';
import { Type } from 'class-transformer';
import { DependencyStatus, TodoPriority, TodoStatus } from '../types';

export enum SortBy {
  DUE_DATE = 'dueDate',
  PRIORITY = 'priority',
  STATUS = 'status',
  NAME = 'name',
}

export enum SortOrder {
  DESC = 'DESC',
  ASC = 'ASC',
}

export class SearchTodoDto {
  @ApiPropertyOptional({ example: 'report' })
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ enum: TodoStatus, example: TodoStatus.NOT_STARTED })
  @IsOptional()
  @IsEnum(TodoStatus)
  status?: TodoStatus;

  @ApiPropertyOptional({ enum: TodoPriority, example: TodoPriority.HIGH })
  @IsOptional()
  @IsEnum(TodoPriority)
  priority?: TodoPriority;

  @ApiPropertyOptional({
    example: '2026-03-01T00:00:00.000Z',
    format: 'date-time',
  })
  @IsOptional()
  @IsDateString()
  dueDateStart?: string;

  @ApiPropertyOptional({
    example: '2026-03-31T23:59:59.999Z',
    format: 'date-time',
  })
  @IsOptional()
  @IsDateString()
  dueDateEnd?: string;

  @ApiPropertyOptional({
    enum: DependencyStatus,
    example: DependencyStatus.BLOCKED,
  })
  @IsOptional()
  @IsEnum(DependencyStatus)
  dependencyStatus?: DependencyStatus;

  @ApiPropertyOptional({ enum: SortBy, default: SortBy.DUE_DATE })
  @IsEnum(SortBy)
  sortBy: SortBy = SortBy.DUE_DATE;

  @ApiPropertyOptional({ enum: SortOrder, default: SortOrder.DESC })
  @IsEnum(SortOrder)
  sortOrder: SortOrder = SortOrder.DESC;

  @ApiPropertyOptional({ example: 1, default: 1, minimum: 1 })
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page: number = 1;

  @ApiPropertyOptional({ example: 10, default: 10, minimum: 10 })
  @Type(() => Number)
  @IsInt()
  @Min(10)
  limit: number = 10;
}
