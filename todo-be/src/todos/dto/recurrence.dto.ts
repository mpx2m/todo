import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsEnum, IsInt, Min, ValidateIf } from 'class-validator';
import { Recurrence, RecurrenceUnit } from '../types';

export class RecurrenceDto {
  @ApiProperty({ enum: Recurrence, example: Recurrence.DAILY })
  @IsEnum(Recurrence)
  type: Recurrence;

  @ApiPropertyOptional({ example: 2, minimum: 1 })
  @ValidateIf((o: RecurrenceDto) => o.type === Recurrence.CUSTOM)
  @Type(() => Number)
  @IsInt()
  @Min(1)
  interval?: number;

  @ApiPropertyOptional({ enum: RecurrenceUnit, example: RecurrenceUnit.DAY })
  @ValidateIf((o: RecurrenceDto) => o.type === Recurrence.CUSTOM)
  @IsEnum(RecurrenceUnit)
  unit?: RecurrenceUnit;
}
